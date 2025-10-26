import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Recipe } from '../models/recipe.model';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RecipeService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getAllRecipes(): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(`${this.apiUrl}`);
  }

  getRecipeById(id: number): Observable<Recipe> {
    return this.http.get<Recipe>(`${this.apiUrl}/${id}`);
  }

  createRecipe(recipe: Recipe): Observable<Recipe> {
    return this.http.post<Recipe>(`${this.apiUrl}`, recipe);
  }

  updateRecipe(id: number, recipe: Recipe): Observable<Recipe> {
    return this.http.put<Recipe>(`${this.apiUrl}/${id}`, recipe);
  }

  deleteRecipe(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  // ✅ Correct search methods
  searchByName(name: string): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(`${this.apiUrl}/search`, {
      params: { name }
    });
  }

  searchByIngredient(ingredient: string): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(`${this.apiUrl}/search`, {
      params: { ingredient }
    });
  }

  getFavoriteRecipes(): Observable<Recipe[]> {
  return this.http.get<Recipe[]>(`${this.apiUrl}/favorites`);
}

// toggleFavorite(recipe: Recipe): Observable<Recipe> {
//   const updatedRecipe = { ...recipe, favorite: !recipe.favorite };
//   return this.http.put<Recipe>(`${this.apiUrl}/${recipe.id}`, updatedRecipe);
// }

toggleFavorite(recipe: Recipe): Observable<Recipe> {
  return this.http.post<Recipe>(
    `${this.apiUrl}/${recipe.id}/favorite`,
    { favorite: !recipe.favorite }   // ✅ send only favorite field
  );
}


}
