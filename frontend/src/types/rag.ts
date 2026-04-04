import { z } from "zod";
import type { DocumentSchema, LmmResponseBaseSchema, LmmResponseSchema, MetadataSchema } from "./schemas";

/**
 * Representa uma pergunta de RAG (Retrieval-Augmented Generation).
 */
export type RagQuestion = {
  /** Identificador único da pergunta */
  id: string;

  /** Texto da pergunta */
  question: string | Blob;

  /** Timestamp do item */
  timestamp: Date;
};

/**
 * Metadados de um documento recuperado durante o RAG.
 */
export type Metadata = z.infer<typeof MetadataSchema>;

/**
 * Documento recuperado durante o RAG.
 */
export type Document = z.infer<typeof DocumentSchema>;

/**
 * Base comum para respostas do LMM.
 */
export type LmmBase = z.infer<typeof LmmResponseBaseSchema>;

/**
 * Resposta do LMM.
 */
export type LmmResponse = z.infer<typeof LmmResponseSchema>;