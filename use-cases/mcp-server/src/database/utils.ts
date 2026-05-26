import postgres from "postgres";
import { getDb } from "./connection";

/**
 * Execute a database operation with proper connection management
 * Following the pattern from BASIC-DB-MCP.md but adapted for PostgreSQL
 */
export async function withDatabase<T>(
	databaseUrl: string,
	operation: (db: postgres.Sql) => Promise<T>
): Promise<T> {
	const db = getDb(databaseUrl);
	const startTime = Date.now();
	try {
		const result = await operation(db);
		const duration = Date.now() - startTime;
		console.log(`Database operation completed successfully in ${duration}ms`);
		return result;
	} catch (error) {
		const duration = Date.now() - startTime;
		console.error(`Database operation failed after ${duration}ms:`, error);
		// Re-throw the error so it can be caught by Sentry in the calling code
		throw error;
	}
	// Note: With PostgreSQL connection pooling, we don't close individual connections
	// They're returned to the pool automatically. The pool is closed when the Durable Object shuts down.
}