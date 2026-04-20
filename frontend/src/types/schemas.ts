import { z } from "zod";

/**
 * Esquema para resposta de erro.
 */
export const ErrorSchema = z.object({
  data: z.string(),
  timestamp: z.coerce.date(),
  type: z.literal("error"),
});

/**
 * Esquema para representar um arquivo armazenado no Object Storage.
 */
export const ObjectSchema = z.object({
  key: z.string(),
  url: z.string(),
  include_in_prompt: z.boolean()
})

/**
 * Metadados de um documento recuperado durante o RAG.
 */
export const MetadataSchema = z.object({
  type: z.string(),
  chunk: z.string().nullable().optional(),
  source: z.string(),
  object: ObjectSchema,
});

/**
 * Documento recuperado durante o RAG.
 */
export const DocumentSchema = z.object({
  metadata: MetadataSchema,
  score: z.number(),
  rerank_score: z.number().nullable().optional(),
});

/**
 * Base comum para respostas do LMM.
 */
export const LmmResponseBaseSchema = z.object({
  questionId: z.string(),
  type: z.union([
    z.literal("text"),
    z.literal("binary"),
    z.literal("error"),
    z.literal("end"),
  ]),
  error_message: z.string().nullable().optional(),
  timestamp: z.coerce.date(),
});

/**
 * Resposta do LMM para casos de sucesso (text, binary, end).
 */
export const LmmSuccessResponseSchema = LmmResponseBaseSchema.extend({
  type: z.union([
    z.literal("text"),
    z.literal("binary"),
    z.literal("end"),
  ]),
  data: z.string(),
  mime_type: z.string().nullable().optional(),
  documents: z.array(DocumentSchema),
});

/**
 * Resposta do LMM para erro.
 * `documents` é opcional nesse caso.
 */
export const LmmErrorResponseSchema = LmmResponseBaseSchema.extend({
  questionId: z.string().optional(),
  type: z.literal("error"),
  data: z.string(),
  mime_type: z.string().nullable().optional(),
  documents: z.array(DocumentSchema).optional(),
});

/**
 * Schema discriminado de resposta do LMM baseado no campo `type`.
 */
export const LmmResponseSchema = z.discriminatedUnion("type", [
  LmmSuccessResponseSchema,
  LmmErrorResponseSchema,
]);

/** Esquema para resposta de ingestão de vetores */
export const IngestResultSchema = z.object({
  chunks_stored: z.number()
});