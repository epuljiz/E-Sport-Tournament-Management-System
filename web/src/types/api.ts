export interface BackendGreska {
  code?: string;
  message?: string;
}

export interface Player {
  id: number;
  nickname: string;
  first_name: string;
  last_name: string;
  position: string;
  birth_date: string;
  nationality?: string;
  team_id: number;
}

export interface Team {
  id: number;
  name: string;
  organization_name: string;
  created_at: string;
  admin_username?: string;
}

export interface Tournament {
  id: number;
  name: string;
  game: string;
  start_date: string;
  location: string;
  prelim_deadline: string;
  final_deadline: string;
}

export interface Registration {
  id: number;
  team_id: number;
  tournament_id: number;
  registration_date: string;
  team_name?: string;
}
