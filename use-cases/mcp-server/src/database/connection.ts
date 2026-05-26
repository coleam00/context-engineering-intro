import postgres from "postgres";

let dbInstance: postgres.Sql | null = null;

/**
 * Get database connection singleton
 * Following the pattern from BASIC-DB-MCP.md but adapted for PostgreSQL with connection pooling
 */
export function getDb(databaseUrl: string): postgres.Sql {
	if (!dbInstance) {
		dbInstance = postgres(databaseUrl, {
			// Connection pool settings for Cloudflare Workers
			max: 5, // Maximum 5 connections to fit within Workers' limit of 6 concurrent connections
			idle_timeout: 20,
			connect_timeout: 10,
			// Enable prepared statements for better performance
			prepare: true,
		});
	}
	return dbInstance;
}

/**
 * Close database connection pool
 * Call this when the Durable Object is shutting down
 */
export async function closeDb(): Promise<void> {
	if (dbInstance) {
		try {
			await dbInstance.end();
		} catch (error) {
			console.error('Error closing database connection:', error);
		} finally {
			dbInstance = null;
		}
	}
}