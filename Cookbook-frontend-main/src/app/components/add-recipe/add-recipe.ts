import { Component } from '@angular/core';
import { Recipe } from '../../models/recipe.model';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RecipeService } from '../../services/recipe.service';

@Component({
  selector: 'app-add-recipe',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './add-recipe.html',
  styleUrls: ['./add-recipe.scss']
})
export class AddRecipe {

  constructor(private recipeService: RecipeService) {} // ✅ Inject service

  recipe: Recipe = {
    name: '',
    description: '',
    ingredients: [''],
    instructions: '',
    favorite: false,
    imageUrl: ''
  };

  addIngredient() {
    this.recipe.ingredients.push('');
  }

  removeIngredient(index: number) {
    this.recipe.ingredients.splice(index, 1);
  }

  onImageSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this.recipe.imageUrl = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  trackByIndex(index: number, item: any): number {
    return index;
  }


  onSubmit() {
    this.recipeService.createRecipe(this.recipe).subscribe({
      next: (res) => {
        console.log('Recipe submitted:', res);
        alert('Recipe submitted successfully!');
        this.recipe = {
          name: '',
          description: '',
          ingredients: [''],
          instructions: '',
          favorite: false,
          imageUrl: ''
        };
      },
      error: (err) => {
        console.error('Failed to submit recipe:', err);
        alert('Error submitting recipe.');
      }
    });
  }
}


