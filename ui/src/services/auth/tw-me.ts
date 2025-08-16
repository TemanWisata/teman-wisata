import axios, { type AxiosResponse } from 'axios';

export interface User {
  id: string;
  user_id: number;
  username: string;
  dob: string;
  full_name?: string | null;
  province: string;
  created_at?: string | null;
  updated_at?: string | null;
  deleted_at?: string | null;
}

export interface MeResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: User | null;
}

export async function getMe(): Promise<MeResponse> {
  const access_token = localStorage.getItem('access_token');
  const token_type = localStorage.getItem('token_type') || 'bearer';

  if (!access_token) {
    return {
      success: false,
      http_status: 401,
      message: 'No access token found',
      data: null,
    };
  }

  try {
    const response: AxiosResponse<MeResponse> = await axios.get('/api/v1/me', {
      headers: {
        Authorization: `${token_type} ${access_token}`,
      },
    });
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as MeResponse;
    }
    throw error;
  }
}
