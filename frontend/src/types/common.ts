import { z } from "zod";
import type { ErrorSchema } from "./schemas";

/** Tipo para representar um erro. */
export type Error = z.infer<typeof ErrorSchema>;