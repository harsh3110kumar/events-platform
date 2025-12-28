const TOKEN_KEY = 'auth_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY)
}

export const getRefreshToken = () => {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

export const setTokens = (access, refresh) => {
  localStorage.setItem(TOKEN_KEY, access)
  if (refresh) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
  }
}

export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

export const authHeaders = () => {
  const token = getToken()
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

