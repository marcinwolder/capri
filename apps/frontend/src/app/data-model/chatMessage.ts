export interface ChatMessage {
  content: string;
  role: 'user' | 'system' | 'assistant';
}
