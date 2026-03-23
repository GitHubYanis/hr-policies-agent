import { Component, signal, inject, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { SUGGESTED_QUESTIONS } from './suggestions.constants';
import { AskResponse, HrChatService, Source } from './hr-chat.service';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  loading?: boolean;
  error?: boolean;
}

@Component({
  selector: 'app-hr-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './hr-chat.component.html',
  styleUrl: './hr-chat.component.css',
})
export class HrChatComponent implements AfterViewChecked {
  @ViewChild('messagesEnd') private messagesEnd!: ElementRef;

  protected readonly suggestedQuestions = SUGGESTED_QUESTIONS;
  protected readonly messages = signal<ChatMessage[]>([]);
  protected readonly isLoading = signal(false);
  protected readonly backendStatus = signal<'unknown' | 'ready' | 'error'>('unknown');

  private _inputText = '';
  get inputTextModel(): string { return this._inputText; }
  set inputTextModel(v: string) { this._inputText = v; }

  private readonly chatService = inject(HrChatService);

  constructor() {
    this.checkBackend();
  }

  ngAfterViewChecked() { this.scrollToBottom(); }

  private scrollToBottom() {
    try { this.messagesEnd?.nativeElement.scrollIntoView({ behavior: 'smooth' }); } catch {}
  }

  private checkBackend() {
    this.chatService.health().subscribe({
      next: (h) => {
        this.backendStatus.set(h.status === 'ready' ? 'ready' : 'error');
      },
      error: () => this.backendStatus.set('error')
    });
  }

  protected useSuggestion(q: string) {
    this._inputText = q;
    this.send();
  }

  protected onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); this.send(); }
  }

  protected send() {
    const q = this._inputText.trim();
    if (!q || this.isLoading()) return;

    this._inputText = '';
    this.isLoading.set(true);

    const userMsg: ChatMessage = { role: 'user', content: q };
    const loadingMsg: ChatMessage = { role: 'assistant', content: '', loading: true };
    this.messages.update(msgs => [...msgs, userMsg, loadingMsg]);

    this.chatService.ask(q).subscribe({
      next: (res: AskResponse) => {
        this.messages.update(msgs => {
          const updated = [...msgs];
          updated[updated.length - 1] = { role: 'assistant', content: res.answer, sources: res.sources, loading: false };
          return updated;
        });
        this.isLoading.set(false);
      },
      error: () => {
        this.messages.update(msgs => {
          const updated = [...msgs];
          updated[updated.length - 1] = {
            role: 'assistant',
            content: "Une erreur s'est produite. Vérifiez que le serveur backend est démarré.",
            loading: false, error: true,
          };
          return updated;
        });
        this.isLoading.set(false);
      }
    });
  }

  protected clearHistory() { this.messages.set([]); }

  protected readonly showSuggestions = () => this.messages().length === 0 && !this.isLoading();

  protected formatContent(raw: string): string {
    return (raw ?? '')
      .replace(/^Réponse\s*:\s*/i, '')
      .replace(/\n*Sources\s*:[\s\S]*$/i, '')
      .trim();
  }
}