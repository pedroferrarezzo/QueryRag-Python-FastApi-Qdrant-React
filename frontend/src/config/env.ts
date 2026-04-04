import { z } from 'zod';

const envSchema = z.object({
  VITE_WS_CHAT_ENDPOINT: z.url("VITE_WS_CHAT_ENDPOINT precisa ser uma URL válida")
});

const _env = envSchema.safeParse(import.meta.env);

if (_env.success === false) {
  throw new Error(`Variáveis de ambiente inválidas.`);
}

export const env = _env.data;