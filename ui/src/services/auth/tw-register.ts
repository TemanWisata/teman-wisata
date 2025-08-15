import axios, { type AxiosResponse } from 'axios';

export interface RegisterPayload {
  username: string;
  password: string;
  dob: string;
  full_name: string;
  province: string;
}

export interface RegisterResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: Record<string, unknown>;
}

export async function registerUser(
  payload: RegisterPayload
): Promise<RegisterResponse> {
  try {
    const response: AxiosResponse<RegisterResponse> = await axios.post(
      'http://127.0.0.1:8000/api/v1/auth/register',
      payload,
      { headers: { 'Content-Type': 'application/json' } }
    );
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as RegisterResponse;
    }
    throw error;
  }
}

// (async () => {
//   const result = await registerUser({
//     username: 'Yourusername',
//     password: 'test1234',
//     dob: '2000-01-01',
//     full_name: 'Your Full Name',
//     province: 'Your Province',
//   });
//   console.log(result);
// })();
