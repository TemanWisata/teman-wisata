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

export interface TopPlaceByProvince {
  province: string;
  places: TopPlaceRating[];
}

export interface TopPlaceProvinceResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: TopPlaceByProvince[] | [];
}

export async function getTopPlaceByProvince(): Promise<TopPlaceProvinceResponse> {
  const access_token = localStorage.getItem('access_token');
  const token_type = localStorage.getItem('token_type') || 'bearer';

  if (!access_token) {
    window.location.href = '/';
    return {
      success: false,
      http_status: 401,
      message: 'No access token found',
      data: [],
    };
  }

  try {
    const response: AxiosResponse<TopPlaceProvinceResponse> = await axios.get(
      '/api/v1/place/top/province',
      {
        headers: {
          Authorization: `${token_type} ${access_token}`,
        },
      }
    );
    console.log(response.status);
    if (response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      window.location.href = '/'; // Redirect to login/home
      return {
        success: false,
        http_status: 401,
        message: 'Token expired or invalid',
        data: [],
      };
    }
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as TopPlaceProvinceResponse;
    }
    throw error;
  }
}
