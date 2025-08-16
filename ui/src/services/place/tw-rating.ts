import axios, { type AxiosResponse } from 'axios';

export interface UserRatingRequest {
  place_id: number;
  rating: number;
}

export interface UserRating {
  user_id: number;
  place_id: number;
  rating: number;
}

export interface RatingResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: UserRating | null;
}

/**
 * Submit a rating for a place.
 * Requires Authorization header with Bearer token.
 */
export async function ratePlace(
  payload: UserRatingRequest,
  token: string
): Promise<RatingResponse> {
  try {
    const response: AxiosResponse<RatingResponse> = await axios.post(
      '/api/v1/place/rate',
      payload,
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      window.location.href = '/'; // Redirect to login/home
      return {
        success: false,
        http_status: 401,
        message: 'Token expired or invalid',
        data: null,
      };
    }
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as RatingResponse;
    }
    throw error;
  }
}

/**
 * Get the current user's rating for a place.
 * Requires Authorization header with Bearer token.
 */
export async function getUserRating(
  place_id: number,
  token: string
): Promise<RatingResponse> {
  try {
    const response: AxiosResponse<RatingResponse> = await axios.get(
      `/api/v1/place/rate/${place_id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as RatingResponse;
    }
    throw error;
  }
}
