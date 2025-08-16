import axios, { type AxiosResponse } from 'axios';

export interface TopPlaceRating {
  id: string;
  place_id: number;
  place_name: string;
  category: string;
  description?: string | null;
  province: string;
  avg_rating: number;
  rating_count: number;
  rank?: number | null;
}

export interface ResponseTopPlaceRating {
  places: TopPlaceRating[];
}

export interface TopPlacesApiResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: ResponseTopPlaceRating | null;
}

export async function getTopPlaces(): Promise<TopPlacesApiResponse> {
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
    const response: AxiosResponse<TopPlacesApiResponse> = await axios.get(
      '/api/v1/place/top',
      {
        headers: {
          Authorization: `${token_type} ${access_token}`,
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
        data: { places: [] },
      };
    }
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as TopPlacesApiResponse;
    }
    throw error;
  }
}

// const result = await getTopPlaces();
// if (result.success && result.data) {
//   console.log(result.data.places);
// } else {
//   console.error(result.message);
// }
