
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import {
  Component,
  Input,
  Output,
  EventEmitter,
  ViewChild,
  ElementRef,
  OnInit,
  SimpleChanges,
  ChangeDetectorRef,
} from "@angular/core";
import { ChatMessage } from "src/app/data/rag-playground-data";

@Component({
  selector: "chat-window",
  templateUrl: "./chat-window.component.html",
  styleUrls: ["./chat-window.component.scss"],
})
export class ChatWindowComponent implements OnInit {
  @Input() messages: any[] = [];

  @Input()
  set disableChat(value: boolean) {
    this.model.disableChat = value;
  }

  @Input()
  set waitingForAPI(value: boolean) {
    this.model.waitingForAPI = value;
  }

  @Input()
  set selectedMessage(selectedMessage: ChatMessage) {
    this.model.selectedMessage = selectedMessage;
  }

  @Output() selectedMessageChange = new EventEmitter<ChatMessage>();
  @Output() sendMessage = new EventEmitter<string>();
  @Output() clearMessages = new EventEmitter();

  @ViewChild("chatMessages") private chatMessagesContainer: ElementRef;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.scrollToBottom();
  }

  model = {
    messageText: "",
    disableChat: true,
    waitingForAPI: false,
    selectedMessage: undefined,
  };

  ngOnChanges(changes: SimpleChanges) {
    if (changes.messages) {
      this.cdr.detectChanges();
      this.scrollToBottom();
    }
  }

  onMessageClick(message: any) {
    this.model.selectedMessage = message;
    this.selectedMessageChange.emit(message);
  }

  submitSearch() {
    if (this.model.messageText.trim() !== "") {
      this.sendMessage.emit(this.model.messageText);
      this.model.messageText = "";
      this.scrollToBottom();
    }
  }

  handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      event.preventDefault();
      this.submitSearch();
    }
  }

  handleClearMessages(event: Event) {
    this.clearMessages.emit();
    (event.target as HTMLElement).blur();
  }

  scrollToBottom(): void {
    if (this.chatMessagesContainer) {
      try {
        this.chatMessagesContainer.nativeElement.scrollTop =
          this.chatMessagesContainer.nativeElement.scrollHeight;
      } catch (err) {
        console.error("Error scrolling to bottom:", err);
      }
    }
  }
}
