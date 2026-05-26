import type { McpResponse } from '../../src/types'

export const mockSuccessResponse: McpResponse = {
  content: [
    {
      type: 'text',
      text: '**Success**\n\nOperation completed successfully',
    },
  ],
}

export const mockErrorResponse: McpResponse = {
  content: [
    {
      type: 'text',
      text: '**Error**\n\nSomething went wrong',
      isError: true,
    },
  ],
}

export const mockQueryResponse: McpResponse = {
  content: [
    {
      type: 'text',
      text: '**Query Results**\n```sql\nSELECT * FROM users\n```\n\n**Results:**\n```json\n[\n  {\n    "id": 1,\n    "name": "John Doe"\n  }\n]\n```\n\n**Rows returned:** 1',
    },
  ],
}

export const mockTableListResponse: McpResponse = {
  content: [
    {
      type: 'text',
      text: '**Database Tables and Schema**\n\n[\n  {\n    "name": "users",\n    "schema": "public",\n    "columns": [\n      {\n        "name": "id",\n        "type": "integer",\n        "nullable": false,\n        "default": "nextval(\'users_id_seq\'::regclass)"\n      }\n    ]\n  }\n]\n\n**Total tables found:** 1\n\n**Note:** Use the `queryDatabase` tool to run SELECT queries, or `executeDatabase` tool for write operations (if you have write access).',
    },
  ],
}