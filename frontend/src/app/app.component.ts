import { Component } from '@angular/core';
import { DecimalPipe, KeyValuePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CATEGORICAL_FIELDS, NUMERIC_FIELDS, SAMPLE } from './features';

interface Result {
  prediction: string;
  confidence: number;
  probabilities: Record<string, number>;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule, KeyValuePipe, DecimalPipe],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  numericFields = NUMERIC_FIELDS;
  categoricalFields = CATEGORICAL_FIELDS;
  form: Record<string, number | string> = { ...SAMPLE };

  isDemo = !['localhost', '127.0.0.1'].includes(window.location.hostname);
  loading = false;
  result: Result | null = null;
  error = '';

  constructor(private http: HttpClient) {}

  loadSample() {
    this.form = { ...SAMPLE };
  }

  predict() {
    this.loading = true;
    this.result = null;
    this.error = '';
    this.http.post<Result>('/api/predict', this.form).subscribe({
      next: (r) => { this.result = r; this.loading = false; },
      error: (e) => {
        this.loading = false;
        this.error = e?.error?.error
          ?? 'Backend not reachable. Start the Flask server (python backend/app.py) and run the UI with npm start.';
      },
    });
  }
}
