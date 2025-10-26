import { Component, OnInit } from '@angular/core';
import { RecipeService } from '../../services/recipe.service';
import { Recipe } from '../../models/recipe.model';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; 

@Component({
  selector: 'app-view-recipes',
  imports: [CommonModule,FormsModule,RouterModule],
  templateUrl: './view-recipes.html',
  standalone: true,
  styleUrls: ['./view-recipes.scss']
})
export class ViewRecipesComponent implements OnInit {
  allRecipes: Recipe[] = [];
  randomRecipes: Recipe[] = [];
  searchByNameText: string = '';
  searchByIngredientText: string = '';

  constructor(private recipeService: RecipeService) {}

  ngOnInit() {
    this.loadRecipes();
  }

  loadRecipes() {
    this.recipeService.getAllRecipes().subscribe((recipes: Recipe[]) => {
      this.allRecipes = recipes;
      this.randomRecipes = this.getRandomRecipes(recipes, 6); // show 6 random recipes
    });
  }

  getRandomRecipes(recipes: Recipe[], count: number): Recipe[] {
    const shuffled = [...recipes].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
  }

  searchByName(): void {
    if (!this.searchByNameText) {
      this.loadRecipes();
      return;
    }

    this.recipeService.searchByName(this.searchByNameText).subscribe((results: Recipe[]) => {
      this.randomRecipes = results;
    });
  }

  searchByIngredient(): void {
    if (!this.searchByIngredientText) {
      this.loadRecipes();
      return;
    }

    this.recipeService.searchByIngredient(this.searchByIngredientText).subscribe((results: Recipe[]) => {
      this.randomRecipes = results;
    });
  }
}
