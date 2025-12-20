import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  Output,
  SimpleChanges
} from '@angular/core';

type StepState = 'pending' | 'active' | 'done';

interface ChecklistStep {
  key: string;
  label: string;
  detail?: string;
  minMs: number;
  maxMs: number;
}

interface ChecklistStepState extends ChecklistStep {
  duration: number;
  state: StepState;
}

@Component({
  selector: 'app-loading-checklist',
  templateUrl: './loading-checklist.component.html',
  styleUrls: ['./loading-checklist.component.css']
})
export class LoadingChecklistComponent implements OnInit, OnDestroy, OnChanges {
  @Input() accelerate = false;
  @Input() cancelled = false;
  @Input() steps: ChecklistStep[] = [
    {
      key: 'analyze-preferences',
      label: 'Analyzing your preferences',
      detail: 'Checking travel dates, pace, and must-haves.',
      minMs: 500,
      maxMs: 2500
    },
    {
      key: 'select-attractions',
      label: 'Selecting must-see places',
      detail: 'Sifting through attractions and local gems.',
      minMs: 700,
      maxMs: 2800
    },
    {
      key: 'arrange-days',
      label: 'Arranging days and routes',
      detail: 'Balancing travel times and grouping nearby spots.',
      minMs: 900,
      maxMs: 3000
    },
    {
      key: 'apply-algorithms',
      label: 'Applying add/remove/edit rules',
      detail: 'Optimizing order with our POI algorithm.',
      minMs: 1000,
      maxMs: 3200
    },
    {
      key: 'write-descriptions',
      label: 'Writing day descriptions',
      detail: 'Summarizing each stop with our LLM.',
      minMs: 1200,
      maxMs: 3500
    }
  ];

  @Output() completed = new EventEmitter<void>();

  stepsState: ChecklistStepState[] = [];
  activeIndex = -1;

  private shouldFastForward = false;
  private timerHandle: number | null = null;
  private completedEmitted = false;

  ngOnInit(): void {
    this.resetSteps();
    this.runStep(0);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['accelerate'] && this.accelerate) {
      this.fastForward();
    }
    if (changes['cancelled'] && this.cancelled) {
      this.clearTimer();
    }
  }

  ngOnDestroy(): void {
    this.clearTimer();
  }

  get progressPercent(): string {
    const total = this.stepsState.length || 1;
    const doneCount = this.stepsState.filter(step => step.state === 'done').length;
    const inProgress = this.activeIndex >= 0 && this.activeIndex < total ? 0.4 : 0;
    const percent = Math.min(100, ((doneCount + inProgress) / total) * 100);
    return `${percent}%`;
  }

  private resetSteps(): void {
    this.stepsState = this.steps.map(step => ({
      ...step,
      duration: this.randomDuration(step.minMs, step.maxMs),
      state: 'pending'
    }));
    this.activeIndex = -1;
    this.completedEmitted = false;
    this.shouldFastForward = false;
    this.clearTimer();
  }

  private runStep(index: number): void {
    if (this.cancelled) {
      return;
    }
    if (index >= this.stepsState.length) {
      this.emitCompleted();
      return;
    }

    this.activeIndex = index;
    this.stepsState[index].state = 'active';
    const duration = this.shouldFastForward ? this.fastDuration() : this.stepsState[index].duration;
    this.clearTimer();
    this.timerHandle = window.setTimeout(() => {
      this.stepsState[index].state = 'done';
      this.runStep(index + 1);
    }, duration);
  }

  private fastForward(): void {
    this.shouldFastForward = true;
    if (this.activeIndex >= 0 && this.activeIndex < this.stepsState.length) {
      this.runStep(this.activeIndex);
    }
  }

  private fastDuration(): number {
    return 180 + Math.floor(Math.random() * 90);
  }

  private emitCompleted(): void {
    if (this.completedEmitted) {
      return;
    }
    this.completedEmitted = true;
    this.activeIndex = -1;
    this.clearTimer();
    this.completed.emit();
  }

  private randomDuration(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  private clearTimer(): void {
    if (this.timerHandle !== null) {
      clearTimeout(this.timerHandle);
      this.timerHandle = null;
    }
  }
}
