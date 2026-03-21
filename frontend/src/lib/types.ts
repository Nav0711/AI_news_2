export interface User {
  email: string;
  profile_type: string | null;
  interests: string[];
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
}

export interface OnboardingData {
  profile_type: string;
  interests: string[];
}
