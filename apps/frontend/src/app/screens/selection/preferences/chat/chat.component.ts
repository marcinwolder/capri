import {AfterViewChecked, Component, ElementRef, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {ChatService} from "../../../../services/chat.service";
import {ChatMessage} from "../../../../data-model/chatMessage";
import {Router} from "@angular/router";
import {DestinationService} from "../../../../services/destination.service";
import {Categories} from "../../../../data-model/categories";
import {RecommendationService} from "../../../../services/recommendation.service";
import {ServiceStatusService} from "../../../../services/service-status.service";
import {combineLatest, map, Observable, Subscription} from "rxjs";
import {environment} from "../../../../../environments/environment";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewChecked, OnDestroy {
  constructor(private _router: Router, private destinationService: DestinationService,
              private chatService: ChatService, private recommendationService: RecommendationService,
              private serviceStatus: ServiceStatusService) {
  }

  serviceStatus$!: Observable<{ backendOffline: boolean; llamaOffline: boolean }>;
  checkingServices$!: Observable<boolean>;
  backendHost = environment.backendHost.replace(/\/$/, '');
  llamaHost = environment.llamaHost.replace(/\/$/, '');
  private statusSubscription?: Subscription;
  private isOffline = false;

  ngOnInit(): void {
    this.serviceStatus$ = combineLatest([
      this.serviceStatus.backendOffline$,
      this.serviceStatus.llamaOffline$
    ]).pipe(
      map(([backendOffline, llamaOffline]) => ({backendOffline, llamaOffline}))
    );
    this.checkingServices$ = this.serviceStatus.checking$;

    this.statusSubscription = this.serviceStatus$.subscribe(status => {
      this.isOffline = status.backendOffline || status.llamaOffline;
    });

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

  ngOnDestroy(): void {
    this.statusSubscription?.unsubscribe();
  }

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
    if (!this.userMessage.trim() || this.writingMessage || this.isOffline) {
      return;
    }
    this.messages.push({
      content: this.userMessage,
      role: 'user'
    });
    this.userMessage = '';
    this.writingMessage = true;
    const assistantMessage: ChatMessage = {
      content: '',
      role: 'assistant'
    };
    let assistantIndex = -1;
    this.chatService.streamChatCompletions(this.messages).subscribe({
      next: (content) => {
        if (assistantIndex === -1) {
          this.messages.push(assistantMessage);
          assistantIndex = this.messages.length - 1;
        }
        this.messages[assistantIndex].content += content || '';
      },
      error: () => {
        if (assistantIndex > -1) {
          this.messages.splice(assistantIndex, 1);
        }
        this.writingMessage = false;
      },
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

  retryServices(): void {
    this.serviceStatus.retryNow();
  }
}
