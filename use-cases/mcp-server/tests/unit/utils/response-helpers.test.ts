import { describe, it, expect } from 'vitest'
import { createSuccessResponse, createErrorResponse } from '../../../src/types'

describe('Response Helpers', () => {
  describe('createSuccessResponse', () => {
    it('should create success response with message only', () => {
      const response = createSuccessResponse('Operation completed')
      
      expect(response.content).toHaveLength(1)
      expect(response.content[0].type).toBe('text')
      expect(response.content[0].text).toBe('**Success**\n\nOperation completed')
      expect(response.content[0].isError).toBeUndefined()
    })

    it('should create success response with message and data', () => {
      const data = { id: 1, name: 'Test' }
      const response = createSuccessResponse('User created', data)
      
      expect(response.content).toHaveLength(1)
      expect(response.content[0].type).toBe('text')
      expect(response.content[0].text).toContain('**Success**')
      expect(response.content[0].text).toContain('User created')
      expect(response.content[0].text).toContain('**Result:**')
      expect(response.content[0].text).toContain(JSON.stringify(data, null, 2))
    })

    it('should handle null data', () => {
      const response = createSuccessResponse('Operation completed', null)
      
      expect(response.content[0].text).toContain('**Success**')
      expect(response.content[0].text).toContain('Operation completed')
      expect(response.content[0].text).toContain('**Result:**')
      expect(response.content[0].text).toContain('null')
    })

    it('should handle undefined data', () => {
      const response = createSuccessResponse('Operation completed', undefined)
      
      expect(response.content[0].text).toBe('**Success**\n\nOperation completed')
      expect(response.content[0].text).not.toContain('**Result:**')
    })

    it('should handle complex data objects', () => {
      const data = {
        users: [
          { id: 1, name: 'Alice' },
          { id: 2, name: 'Bob' }
        ],
        meta: {
          total: 2,
          page: 1
        }
      }
      
      const response = createSuccessResponse('Users retrieved', data)
      
      expect(response.content[0].text).toContain('**Success**')
      expect(response.content[0].text).toContain('Users retrieved')
      expect(response.content[0].text).toContain('Alice')
      expect(response.content[0].text).toContain('Bob')
      expect(response.content[0].text).toContain('total')
    })
  })

  describe('createErrorResponse', () => {
    it('should create error response with message only', () => {
      const response = createErrorResponse('Something went wrong')
      
      expect(response.content).toHaveLength(1)
      expect(response.content[0].type).toBe('text')
      expect(response.content[0].text).toBe('**Error**\n\nSomething went wrong')
      expect(response.content[0].isError).toBe(true)
    })

    it('should create error response with message and details', () => {
      const details = { code: 'VALIDATION_ERROR', field: 'email' }
      const response = createErrorResponse('Validation failed', details)
      
      expect(response.content).toHaveLength(1)
      expect(response.content[0].type).toBe('text')
      expect(response.content[0].text).toContain('**Error**')
      expect(response.content[0].text).toContain('Validation failed')
      expect(response.content[0].text).toContain('**Details:**')
      expect(response.content[0].text).toContain(JSON.stringify(details, null, 2))
      expect(response.content[0].isError).toBe(true)
    })

    it('should handle null details', () => {
      const response = createErrorResponse('Operation failed', null)
      
      expect(response.content[0].text).toContain('**Error**')
      expect(response.content[0].text).toContain('Operation failed')
      expect(response.content[0].text).toContain('**Details:**')
      expect(response.content[0].text).toContain('null')
    })

    it('should handle undefined details', () => {
      const response = createErrorResponse('Operation failed', undefined)
      
      expect(response.content[0].text).toBe('**Error**\n\nOperation failed')
      expect(response.content[0].text).not.toContain('**Details:**')
    })

    it('should handle error objects as details', () => {
      const error = new Error('Database connection failed')
      const response = createErrorResponse('Database error', error)
      
      expect(response.content[0].text).toContain('**Error**')
      expect(response.content[0].text).toContain('Database error')
      expect(response.content[0].text).toContain('**Details:**')
      expect(response.content[0].isError).toBe(true)
    })

    it('should handle complex error details', () => {
      const details = {
        error: 'AUTHENTICATION_FAILED',
        message: 'Invalid credentials',
        attempts: 3,
        nextRetryAt: new Date().toISOString()
      }
      
      const response = createErrorResponse('Authentication failed', details)
      
      expect(response.content[0].text).toContain('AUTHENTICATION_FAILED')
      expect(response.content[0].text).toContain('Invalid credentials')
      expect(response.content[0].text).toContain('attempts')
      expect(response.content[0].isError).toBe(true)
    })
  })

  describe('response format consistency', () => {
    it('should maintain consistent structure across response types', () => {
      const successResponse = createSuccessResponse('Success message')
      const errorResponse = createErrorResponse('Error message')
      
      // Both should have the same structure
      expect(successResponse.content).toHaveLength(1)
      expect(errorResponse.content).toHaveLength(1)
      
      expect(successResponse.content[0].type).toBe('text')
      expect(errorResponse.content[0].type).toBe('text')
      
      expect(typeof successResponse.content[0].text).toBe('string')
      expect(typeof errorResponse.content[0].text).toBe('string')
    })

    it('should distinguish between success and error responses', () => {
      const successResponse = createSuccessResponse('Success message')
      const errorResponse = createErrorResponse('Error message')
      
      expect(successResponse.content[0].isError).toBeUndefined()
      expect(errorResponse.content[0].isError).toBe(true)
    })
  })
})