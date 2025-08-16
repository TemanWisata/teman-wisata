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

export interface PlaceResponse {
  success: boolean;
  http_status: number;
  message: string;
  data: Place | null;
}

export async function getPlaceById(id: string): Promise<PlaceResponse> {
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
    const response: AxiosResponse<PlaceResponse> = await axios.get(
      `/api/v1/place/${id}/`,
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
      return error.response.data as PlaceResponse;
    }
    throw error;
  }
}

// async function fetchPlaceById(id: string) {
//   const response = await getPlaceById(id);

//   if (response.success && response.data) {
//     console.log('Place:', response.data);
//   } else {
//     console.error('Error fetching place:', response.message);
//   }
// }

// // Example usage:
// const params = new URLSearchParams(window.location.search);
// const id = params.get('id');
// if (id) {
//   fetchPlaceById(id);
// }
