import { vi } from 'vitest'
import { mockTableColumns, mockQueryResult } from '../fixtures/database.fixtures'

// Mock postgres function
export const mockPostgresInstance = {
  unsafe: vi.fn(),
  end: vi.fn(),
  // Template literal query method
  '`SELECT * FROM users`': vi.fn(),
}

// Mock the postgres module
vi.mock('postgres', () => ({
  default: vi.fn(() => mockPostgresInstance),
}))

// Mock database connection functions
vi.mock('../../src/database/connection', () => ({
  getDb: vi.fn(() => mockPostgresInstance),
  closeDb: vi.fn(),
}))

// Mock database utils
vi.mock('../../src/database/utils', () => ({
  withDatabase: vi.fn(async (url: string, operation: any) => {
    return await operation(mockPostgresInstance)
  }),
}))

// Mock setup functions
export function setupDatabaseMocks() {
  mockPostgresInstance.unsafe.mockImplementation((query: string) => {
    if (query.includes('information_schema.columns')) {
      return Promise.resolve(mockTableColumns)
    }
    if (query.includes('SELECT')) {
      return Promise.resolve(mockQueryResult)
    }
    if (query.includes('INSERT') || query.includes('UPDATE') || query.includes('DELETE')) {
      return Promise.resolve([{ affectedRows: 1 }])
    }
    return Promise.resolve([])
  })
}

export function setupDatabaseError() {
  mockPostgresInstance.unsafe.mockRejectedValue(new Error('Database connection failed'))
}

export function setupDatabaseTimeout() {
  mockPostgresInstance.unsafe.mockRejectedValue(new Error('Connection timeout'))
}

export function resetDatabaseMocks() {
  vi.clearAllMocks()
  setupDatabaseMocks()
}