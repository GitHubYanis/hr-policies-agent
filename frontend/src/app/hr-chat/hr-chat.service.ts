import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Source {
  section_number: string;
  section_title: string;
  page_number: number;
}

export interface AskResponse {
  question: string;
  answer: string;
  sources: Source[];
}

export interface HealthResponse {
  status: string;
  collection_size: number;
  deps_ready: boolean;
}

@Injectable({ providedIn: 'root' })
export class HrChatService {
  private readonly BASE_URL = 'http://localhost:8000';
  private readonly http = inject(HttpClient);

  ask(question: string): Observable<AskResponse> {
    return this.http.post<AskResponse>(`${this.BASE_URL}/ask`, { question });
  }

  health(): Observable<HealthResponse> {
    return this.http.get<HealthResponse>(`${this.BASE_URL}/status`);
  }
}