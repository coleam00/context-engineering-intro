import { vi } from 'vitest'
import { mockAuthRequest, mockClientInfo } from '../fixtures/auth.fixtures'

// Mock OAuth provider
export const mockOAuthProvider = {
  parseAuthRequest: vi.fn(),
  lookupClient: vi.fn(),
  completeAuthorization: vi.fn(),
}

// Mock OAuth helpers
export const mockOAuthHelpers = {
  ...mockOAuthProvider,
}

// Mock Cloudflare Workers OAuth Provider
vi.mock('@cloudflare/workers-oauth-provider', () => ({
  default: vi.fn(() => ({
    fetch: vi.fn(),
  })),
}))

export function setupOAuthMocks() {
  mockOAuthProvider.parseAuthRequest.mockResolvedValue(mockAuthRequest)
  mockOAuthProvider.lookupClient.mockResolvedValue(mockClientInfo)
  mockOAuthProvider.completeAuthorization.mockResolvedValue({
    redirectTo: 'http://localhost:3000/callback?code=success',
  })
}

export function setupOAuthError() {
  mockOAuthProvider.parseAuthRequest.mockRejectedValue(new Error('Invalid OAuth request'))
}

export function resetOAuthMocks() {
  vi.clearAllMocks()
  setupOAuthMocks()
}

// Mock environment with OAuth provider
export const mockEnv = {
  GITHUB_CLIENT_ID: 'test-client-id',
  GITHUB_CLIENT_SECRET: 'test-client-secret',
  COOKIE_ENCRYPTION_KEY: 'test-encryption-key',
  DATABASE_URL: 'postgresql://test:test@localhost:5432/test',
  OAUTH_PROVIDER: mockOAuthProvider,
}