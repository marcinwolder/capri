import {AfterViewChecked, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {ChatService} from "../../../../services/chat.service";
import {ChatMessage} from "../../../../data-model/chatMessage";
import {Router} from "@angular/router";
import {DestinationService} from "../../../../services/destination.service";
import {Categories} from "../../../../data-model/categories";
import {RecommendationService} from "../../../../services/recommendation.service";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  constructor(private _router: Router, private destinationService: DestinationService,
              private chatService: ChatService, private recommendationService: RecommendationService) {
  }

  ngOnInit(): void {
    this.destinationService.setNextFunction(() => {
      this.recommendationService.setMessages(this.messages)
      this._router.navigate(['trip']);
    });

    this.destinationService.setPreviousFunction(() => {
      this._router.navigate(['selection/time']);
    });
  }

  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;
  private isUserScrolling = false;

  messages: ChatMessage[] = [
    {
      content: 'Hello! I am your travel assistant. I am here to help you plan your trip.\n' +
        'Could you please tell me about your preferences.',
      role: 'assistant'
    }
  ];
  userMessage: string = '';
  writingMessage: boolean = false;

  ngAfterViewChecked() {
    if (!this.isUserScrolling) {
      this.scrollToBottom();
    }
  }

  private scrollToBottom(): void {
    try {
      this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
    } catch (err) {
    }
  }

  onUserScroll(): void {
    const {scrollTop, scrollHeight, clientHeight} = this.scrollContainer.nativeElement;
    this.isUserScrolling = scrollHeight - scrollTop > clientHeight + 10;
  }

  async sendChatMessage(): Promise<void> {
    if (!this.userMessage.trim() || this.writingMessage) {
      return;
    }
    this.messages.push({
      content: this.userMessage,
      role: 'user'
    });
    this.userMessage = '';
    this.messages.push({
      content: '',
      role: 'assistant'
    });
    this.writingMessage = true;
    this.chatService.streamChatCompletions(this.messages.slice(0, -1)).subscribe({
      next: (content) => this.messages[this.messages.length - 1].content += content || '',
      error: (error) => this.messages[this.messages.length - 1].content += error,
      complete: () => this.writingMessage = false
    });
  }

  handleEnter(event: Event): void {
    const e = event as KeyboardEvent;
    if (e.key === 'Enter' && !e.shiftKey) {
      event.preventDefault();
      this.sendChatMessage()
    }
  }


  autoGrowTextZone(e: KeyboardEvent) {
    const target = e.target as HTMLTextAreaElement;
    target.style.height = "40px";
    target.style.height = (target.scrollHeight + 2) + "px";
  }
}
