export const mockTableColumns = [
  {
    table_name: 'users',
    column_name: 'id',
    data_type: 'integer',
    is_nullable: 'NO',
    column_default: 'nextval(\'users_id_seq\'::regclass)',
  },
  {
    table_name: 'users',
    column_name: 'name',
    data_type: 'character varying',
    is_nullable: 'YES',
    column_default: null,
  },
  {
    table_name: 'users',
    column_name: 'email',
    data_type: 'character varying',
    is_nullable: 'NO',
    column_default: null,
  },
  {
    table_name: 'posts',
    column_name: 'id',
    data_type: 'integer',
    is_nullable: 'NO',
    column_default: 'nextval(\'posts_id_seq\'::regclass)',
  },
  {
    table_name: 'posts',
    column_name: 'title',
    data_type: 'text',
    is_nullable: 'NO',
    column_default: null,
  },
  {
    table_name: 'posts',
    column_name: 'user_id',
    data_type: 'integer',
    is_nullable: 'NO',
    column_default: null,
  },
]

export const mockQueryResult = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
]

export const mockInsertResult = [
  { id: 3, name: 'New User', email: 'new@example.com' },
]

export const validSelectQuery = 'SELECT * FROM users WHERE id = 1'
export const validInsertQuery = 'INSERT INTO users (name, email) VALUES (\'Test\', \'test@example.com\')'
export const validUpdateQuery = 'UPDATE users SET name = \'Updated\' WHERE id = 1'
export const validDeleteQuery = 'DELETE FROM users WHERE id = 1'

export const dangerousDropQuery = 'DROP TABLE users'
export const dangerousDeleteAllQuery = 'SELECT * FROM users; DELETE FROM users WHERE 1=1'
export const maliciousInjectionQuery = 'SELECT * FROM users; DROP TABLE users; --'
export const emptyQuery = ''
export const whitespaceQuery = '   '