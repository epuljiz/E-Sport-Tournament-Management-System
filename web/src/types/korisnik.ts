export interface KorisnikPodaci {
  id: number;
  username: string;
  role: 'admin' | 'club' | 'team_admin';
  club_id?: number | null;
}
