import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {ChatMessage} from "../data-model/chatMessage";
import {DestinationService} from "./destination.service";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private readonly API_URL = environment.llamaHost + 'v1/chat/completions';

  constructor(private destinationService: DestinationService) {
  }

  public streamChatCompletions(messages: ChatMessage[]): Observable<string | undefined> {
    return new Observable(observer => {
      if (!messages) {
        observer.error('Messages are required.');
        return;
      }

      messages = messages.map(message => {
        return {
          content: this.removeMultipleSpaces(message.content),
          role: message.role
        };
      });
      messages.unshift({
        content: 'You are travel assistant asking about preferences. ' +
          'You are here to help me plan my trip to ' +
          `${this.destinationService.getDestination().city} for ${this.destinationService.getTripLength()} days.` +
          "Ask me about details, activities, preferences and types of places that I enjoy. " +
          "You should suggest places types. " +
          "Do not suggest any places or activities. You are here just to establish my preferences." +
          "You are not allowed under any circumstances even with my permission to send any emails, "+
          "book places ask for accommodation or do anything that required internet access.",
        role: "system"
      })


      const controller = new AbortController();
      const signal = controller.signal;

      fetch(this.API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          messages,
          model: environment.llamaModel,
          max_tokens: 1000,
          temperature: 0.5,
          stream: true,
        }),
        signal
      }).then(response => {
        if (!response.body) {
          observer.error('Response body is missing.');
          return;
        }
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');

        const read = () => {
          reader.read().then(({done, value}) => {
            if (done) {
              observer.complete();
              return;
            }

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            lines.forEach(line => {
              if (line.startsWith('data: ')) {
                const content = line.replace(/^data: /, '').trim();
                if (content && content !== '[DONE]') {
                  try {
                    const parsedContent = JSON.parse(content);
                    observer.next(parsedContent.choices[0].delta.content);
                  } catch (error) {
                    observer.error('Error parsing JSON chunk');
                  }
                }
              }
            });

            read();
          }).catch(error => {
            if (signal.aborted) {
              observer.next('Request aborted.');
            } else {
              observer.error('Error occurred while generating.' + error);
            }
          });
        };

        read();
      }).catch(error => {
        observer.error('Fetch request failed. ' + error);
      });

      return () => controller.abort();
    });

  }

  private removeMultipleSpaces(content: string): string {
    return content.replace(/\s+/g, ' ').trim();
  }
}
