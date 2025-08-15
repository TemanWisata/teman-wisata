import axios, { type AxiosResponse } from 'axios';

export interface LoginPayload {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: 'bearer' | null;
}

export interface LoginResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: Token;
}

export async function loginUser(payload: LoginPayload): Promise<LoginResponse> {
  try {
    const response: AxiosResponse<LoginResponse> = await axios.post(
      '/api/v1/auth/login',
      payload,
      { headers: { 'Content-Type': 'application/json' } }
    );
    // Store token in localStorage for session management
    if (
      response.data.success &&
      response.data.data.access_token &&
      typeof window !== 'undefined' &&
      window.localStorage
    ) {
      localStorage.setItem('access_token', response.data.data.access_token);
      localStorage.setItem('token_type', response.data.data.token_type ?? '');
    }
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as LoginResponse;
    }
    throw error;
  }
}

// // Example usage:
// (async () => {
//   const result = await loginUser({
//     username: 'Yourusername',
//     password: 'test1234',
//   });
//   console.log(result);
// })();
