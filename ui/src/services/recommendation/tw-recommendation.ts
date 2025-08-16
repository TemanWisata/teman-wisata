import axios, { type AxiosResponse } from 'axios';

export interface Place {
  id: string;
  place_id: number;
  place_name: string;
  description?: string | null;
  category: string;
  province: string;
  price?: number | null;
  rating: number;
  time_minutes?: number | null;
  latitude?: number | null;
  longitude?: number | null;
}

export interface RecommendedPlace {
  data: Array<Place | null>;
}

export interface RecommendationResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: RecommendedPlace;
}

export interface RecommenderRequest {
  k?: number;
  filter_viewed?: boolean;
}

/**
 * Get recommended places for the authenticated user.
 * @param payload - Recommendation request payload.
 * @returns Promise with recommendation response.
 */
export async function getUserRecommendations(
  payload: RecommenderRequest = { k: 10, filter_viewed: true }
): Promise<RecommendationResponse> {
  const access_token = localStorage.getItem('access_token');
  const token_type = localStorage.getItem('token_type') || 'bearer';

  if (!access_token) {
    return {
      success: false,
      http_status: 401,
      message: 'No access token found',
      data: { data: [] },
    };
  }

  try {
    const response: AxiosResponse<RecommendationResponse> = await axios.post(
      '/api/v1/recommender/user/',
      payload,
      {
        headers: {
          Authorization: `${token_type} ${access_token}`,
        },
      }
    );
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as RecommendationResponse;
    }
    throw error;
  }
}
