import { describe, it, expect, vi, beforeEach } from 'vitest'

// Mock the database connection module
const mockDbInstance = {
  unsafe: vi.fn(),
  end: vi.fn(),
}

vi.mock('../../../src/database/connection', () => ({
  getDb: vi.fn(() => mockDbInstance),
}))

// Now import the modules
import { withDatabase } from '../../../src/database/utils'

describe('Database Utils', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('withDatabase', () => {
    it('should execute database operation successfully', async () => {
      const mockOperation = vi.fn().mockResolvedValue('success')
      const result = await withDatabase('test-url', mockOperation)
      
      expect(result).toBe('success')
      expect(mockOperation).toHaveBeenCalledWith(mockDbInstance)
    })

    it('should handle database operation errors', async () => {
      const mockOperation = vi.fn().mockRejectedValue(new Error('Operation failed'))
      
      await expect(withDatabase('test-url', mockOperation)).rejects.toThrow('Operation failed')
      expect(mockOperation).toHaveBeenCalledWith(mockDbInstance)
    })

    it('should log successful operations', async () => {
      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
      const mockOperation = vi.fn().mockResolvedValue('success')
      
      await withDatabase('test-url', mockOperation)
      
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringMatching(/Database operation completed successfully in \d+ms/)
      )
      consoleSpy.mockRestore()
    })

    it('should log failed operations', async () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      const mockOperation = vi.fn().mockRejectedValue(new Error('Operation failed'))
      
      await expect(withDatabase('test-url', mockOperation)).rejects.toThrow('Operation failed')
      
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringMatching(/Database operation failed after \d+ms:/),
        expect.any(Error)
      )
      consoleSpy.mockRestore()
    })

    it('should measure execution time', async () => {
      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
      const mockOperation = vi.fn().mockImplementation(async () => {
        // Simulate some delay
        await new Promise(resolve => setTimeout(resolve, 10))
        return 'success'
      })
      
      await withDatabase('test-url', mockOperation)
      
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringMatching(/Database operation completed successfully in \d+ms/)
      )
      consoleSpy.mockRestore()
    })
  })
})