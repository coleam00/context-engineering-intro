import type { SqlValidationResult } from "../types";

/**
 * SQL injection protection: Basic SQL keyword validation
 * This is a simple check - in production you should use parameterized queries
 */
export function validateSqlQuery(sql: string): SqlValidationResult {
	const trimmedSql = sql.trim().toLowerCase();
	
	// Check for empty queries
	if (!trimmedSql) {
		return { isValid: false, error: "SQL query cannot be empty" };
	}
	
	// Check for obviously dangerous patterns
	const dangerousPatterns = [
		/;\s*drop\s+/i,
		/^drop\s+/i, // DROP at start of query
		/;\s*delete\s+.*\s+where\s+1\s*=\s*1/i,
		/;\s*update\s+.*\s+set\s+.*\s+where\s+1\s*=\s*1/i,
		/;\s*truncate\s+/i,
		/^truncate\s+/i, // TRUNCATE at start of query
		/;\s*alter\s+/i,
		/^alter\s+/i, // ALTER at start of query
		/;\s*create\s+/i,
		/;\s*grant\s+/i,
		/;\s*revoke\s+/i,
		/xp_cmdshell/i,
		/sp_executesql/i,
	];
	
	for (const pattern of dangerousPatterns) {
		if (pattern.test(sql)) {
			return { isValid: false, error: "Query contains potentially dangerous SQL patterns" };
		}
	}
	
	return { isValid: true };
}

/**
 * Check if a SQL query is a write operation
 */
export function isWriteOperation(sql: string): boolean {
	const trimmedSql = sql.trim().toLowerCase();
	const writeKeywords = [
		'insert', 'update', 'delete', 'create', 'drop', 'alter', 
		'truncate', 'grant', 'revoke', 'commit', 'rollback'
	];
	
	return writeKeywords.some(keyword => trimmedSql.startsWith(keyword));
}

/**
 * Format database error for user-friendly display
 */
export function formatDatabaseError(error: unknown): string {
	if (error instanceof Error) {
		// Hide sensitive connection details
		if (error.message.includes('password')) {
			return "Database authentication failed. Please check your credentials.";
		}
		if (error.message.includes('timeout')) {
			return "Database connection timed out. Please try again.";
		}
		if (error.message.includes('connection') || error.message.includes('connect')) {
			return "Unable to connect to database. Please check your connection string.";
		}
		return `Database error: ${error.message}`;
	}
	return "An unknown database error occurred.";
}