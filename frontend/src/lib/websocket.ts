import {env} from "../config/env"
import { type Dispatch, type SetStateAction } from "react";
import { LmmResponseSchema } from "@/types/schemas";
import type { ServerConnectionStatus } from "@/types/server";
import type { LmmResponse, RagQuestion } from "@/types/rag";
import { blobToBase64 } from "./utils";

/**
 * Propriedades para a função createWebSocket
 */
type createWebSocketProps = {
    setRagServerConnected: Dispatch<SetStateAction<ServerConnectionStatus>>;
    onOpenCallback?: () => void;
    onCloseCallback?: (event: CloseEvent) => void;
    errorCallback?: (error: any) => void;
}

/**
 * Propriedades para a função configureHandleMessage
 */
type configureHandleMessageProps = {
    ws: WebSocket;
    setLmmResponses: Dispatch<SetStateAction<LmmResponse[]>>;
    setChatInProgress: Dispatch<SetStateAction<boolean>>;
    errorCallback?: (error: any) => void;
    ragServerErrorCallback?: (errorMessage: string) => void;
}

/**
 * Propriedades para a função configureHandleError
 */
type configureHandleErrorProps = {
    ws: WebSocket;
    setChatInProgress: Dispatch<SetStateAction<boolean>>;
}

/** Propriedades para a função sendQuestion
 */
type sendQuestionProps = {
    ws: WebSocket | null;
    lastQuestion: RagQuestion;
    setChatInProgress: Dispatch<SetStateAction<boolean>>;
    errorCallback?: (error: any) => void;
}

/**
 * Cria uma nova instância de WebSocket conectada ao endpoint do RAG Server
 * @returns Instância de WebSocket conectada ao RAG Server
 */
export function createWebSocket(props: createWebSocketProps): WebSocket {
    try {
        props.setRagServerConnected("connecting");

        const ws = new WebSocket(env.VITE_WS_CHAT_ENDPOINT);

        ws.onopen = () => {
            props.setRagServerConnected("connected");
            if (props.onOpenCallback) {
                props.onOpenCallback();
            }
        };

        ws.onclose = (event) => {
            props.setRagServerConnected("disconnected");
            if (props.onCloseCallback) {
                props.onCloseCallback(event);
            }
        };

        return ws;
    }
    catch(err) {
        props.setRagServerConnected("disconnected");
        if (props.errorCallback) {
            props.errorCallback(err);
        }
        throw err;
    }
} 

/** Configura o handler para mensagens recebidas via WebSocket */
export function configureHandleMessage(props: configureHandleMessageProps) {
  props.ws.onmessage = (event) => {
      try{
        const rawLmmResponse = JSON.parse(event.data);
        
        const lmmResponse = LmmResponseSchema.parse(rawLmmResponse);

        if (lmmResponse && lmmResponse.type === "error") {
            props.setChatInProgress(false);
            if (props.ragServerErrorCallback) {
                props.ragServerErrorCallback(lmmResponse.data);
            }
            return;
        }

        if (lmmResponse && lmmResponse.type === "end") {
            props.setChatInProgress(false);
            return;
        }

        props.setLmmResponses(prevLmmResponses => {
            const existingLmmResponseIndex = prevLmmResponses.findIndex(a => a.questionId === lmmResponse.questionId);

            if (existingLmmResponseIndex !== -1) {
                const updatedLmmResponses = [...prevLmmResponses];
                const existingLmmResponse = updatedLmmResponses[existingLmmResponseIndex];
                
                updatedLmmResponses[existingLmmResponseIndex] = {
                    ...existingLmmResponse,
                    data: existingLmmResponse.data + lmmResponse.data 
                };
                
                return updatedLmmResponses;
            }

            return [...prevLmmResponses, { ...lmmResponse }];
        });

      }
      catch(err) {
        props.setChatInProgress(false);
        if (props.errorCallback) {
            props.errorCallback(err);
        }
      }
  };

}

/** Configura o handler para erros de WebSocket */
export function configureHandleError(props: configureHandleErrorProps) {
    props.ws.onerror = () => {
        props.setChatInProgress(false);
    };
}

/** Envia uma pergunta para o RAG Server via WebSocket */
export async function sendQuestion(props: sendQuestionProps) {
    try {
        if (props.ws && props.ws.readyState === WebSocket.OPEN && props.lastQuestion) {
            props.setChatInProgress(true);

            const payload = typeof props.lastQuestion.question === "string"
                ? { prompt: props.lastQuestion.question, questionId: props.lastQuestion.id }
                : { prompt_b64: await blobToBase64(props.lastQuestion.question), questionId: props.lastQuestion.id };

            props.ws.send(JSON.stringify(payload));
        }
    }
    catch(err) {
        props.setChatInProgress(false);
        if (props.errorCallback) {
            props.errorCallback(err);
        }
    }
}