export type Job = {
  id: number;
  title: string;
  company: string;
  time: string;
  tags: string;
  locations: string;
  link: string;
  logo?: string;
  salary_from?: number;
  salary_to?: number;
  currency?: string;
};
