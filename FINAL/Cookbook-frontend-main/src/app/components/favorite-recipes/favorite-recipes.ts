import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecipeService } from '../../services/recipe.service';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-favorite-recipes',
  standalone: true,
  imports: [CommonModule], // ✅ Import CommonModule + directives
  templateUrl: './favorite-recipes.html',
  styleUrls: ['./favorite-recipes.scss']
})
export class FavoriteRecipesComponent {
  favoriteRecipes: Recipe[] = [];

  constructor(private recipeService: RecipeService) {}

  ngOnInit() {
    this.recipeService.getFavoriteRecipes().subscribe({
      next: (data) => this.favoriteRecipes = data,
      error: (err) => console.error('Error fetching favorites', err)
    });
  }
}
