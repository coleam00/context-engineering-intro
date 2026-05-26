import type { Props } from '../../src/types'

export const mockProps: Props = {
  login: 'testuser',
  name: 'Test User',
  email: 'test@example.com',
  accessToken: 'test-access-token',
}

export const mockPrivilegedProps: Props = {
  login: 'coleam00',
  name: 'Cole Medin',
  email: 'cole@example.com',
  accessToken: 'privileged-access-token',
}

export const mockGitHubUser = {
  data: {
    login: 'testuser',
    name: 'Test User',
    email: 'test@example.com',
    id: 12345,
    avatar_url: 'https://github.com/images/avatar.png',
  },
}

export const mockAuthRequest = {
  clientId: 'test-client-id',
  redirectUri: 'http://localhost:3000/callback',
  scope: 'read:user',
  state: 'test-state',
  codeChallenge: 'test-challenge',
  codeChallengeMethod: 'S256',
}

export const mockClientInfo = {
  id: 'test-client-id',
  name: 'Test Client',
  description: 'A test OAuth client',
  logoUrl: 'https://example.com/logo.png',
}

export const mockAccessToken = 'github-access-token-123'
export const mockAuthorizationCode = 'auth-code-456'
export const mockState = 'oauth-state-789'