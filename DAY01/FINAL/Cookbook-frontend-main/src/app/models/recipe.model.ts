export interface Recipe {
  id?: number;
  name: string;
  description: string;
  ingredients: string[];
  instructions: string;
  favorite?: boolean;
  imageUrl?: string;


  // imageUrl?: string; // For simplicity, this will be a base64 string or URL
}
