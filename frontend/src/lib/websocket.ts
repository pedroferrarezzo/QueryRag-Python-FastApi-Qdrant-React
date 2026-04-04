import {env} from "../config/env"
import { type Dispatch, type SetStateAction } from "react";
import { LmmResponseSchema } from "@/types/schemas";
import type { ServerConnectionStatus } from "@/types/server";
import { toast } from "sonner";
import type { LmmResponse, RagQuestion } from "@/types/rag";
import { blobToBase64 } from "./utils";

/**
 * Propriedades para a função createWebSocket
 */
type createWebSocketProps = {
    setRagServerConnected: Dispatch<SetStateAction<ServerConnectionStatus>>;
}

/**
 * Propriedades para a função configureHandleMessage
 */
type configureHandleMessageProps = {
    ws: WebSocket;
    setLmmResponses: Dispatch<SetStateAction<LmmResponse[]>>;
    setChatInProgress: Dispatch<SetStateAction<boolean>>;
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
            toast.info("Conexão WebSocket estabelecida");
        };

        ws.onclose = () => {
            props.setRagServerConnected("disconnected");
            toast.info("Conexão WebSocket encerrada");
        };

        return ws;
    }
    catch(err) {
        props.setRagServerConnected("disconnected");
        toast.error("WebSocket Creating Error: " + err);
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
            toast.error("RAG Server Error: " + lmmResponse.data);
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
        toast.error("WebSocket Processing Error: " + err);
      }
  };

}

/** Configura o handler para erros de WebSocket */
export function configureHandleError(props: configureHandleErrorProps) {
    props.ws.onerror = (error) => {
        props.setChatInProgress(false);
        toast.error("WebSocket Error: " + error);
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
        toast.error("WebSocket Sending Error: " + err);
    }
}