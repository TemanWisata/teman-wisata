import axios, { type AxiosResponse } from 'axios';

export interface Place {
  id?: string | null;
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

export interface PlacesResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: Place[] | null;
}

export interface AllPlaceRequest {
  limit?: number;
  page?: number;
  query_filter?: Record<string, unknown>;
}

export async function getPlaces(
  params: AllPlaceRequest
): Promise<PlacesResponse> {
  const access_token = localStorage.getItem('access_token');
  const token_type = localStorage.getItem('token_type') || 'bearer';

  if (!access_token) {
    window.location.href = '/';
    return {
      success: false,
      http_status: 401,
      message: 'No access token found',
      data: null,
    };
  }

  try {
    const response: AxiosResponse<PlacesResponse> = await axios.post(
      '/api/v1/place/',
      params,
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
        data: null,
      };
    }
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response && error.response.data) {
      return error.response.data as PlacesResponse;
    }
    throw error;
  }
}

// async function fetchPlaces() {
//   const params: AllPlaceRequest = {
//     limit: 10,
//     page: 1,
//   };

//   const response = await getPlaces(params);

//   if (response.success && response.data) {
//     console.log('Places:', response.data);
//   } else {
//     console.error('Error fetching places:', response.message);
//   }
// }

// fetchPlaces();
