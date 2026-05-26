import { beforeEach, vi } from 'vitest'

// Mock crypto API for Node.js environment
Object.defineProperty(global, 'crypto', {
  value: {
    subtle: {
      sign: vi.fn(),
      verify: vi.fn(),
      importKey: vi.fn(),
    },
    getRandomValues: vi.fn(),
  },
})

// Mock fetch globally
global.fetch = vi.fn()

beforeEach(() => {
  vi.clearAllMocks()
})