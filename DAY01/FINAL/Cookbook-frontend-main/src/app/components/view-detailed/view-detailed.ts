// src/app/components/view-detailed/view-detailed.component.ts

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RecipeService } from '../../services/recipe.service';
import { Recipe } from '../../models/recipe.model';
import { CommonModule } from '@angular/common'; 
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-view-detailed',
  imports: [CommonModule, RouterModule],
  templateUrl: './view-detailed.html',
  styleUrls: ['./view-detailed.scss']
})
export class ViewDetailedComponent implements OnInit {
  recipe: Recipe | null = null;

  constructor(
    private route: ActivatedRoute,
    private recipeService: RecipeService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.recipeService.getRecipeById(id).subscribe((data: Recipe) => {
        this.recipe = data;
      });
    }
  }
  toggleFavorite(recipe: Recipe): void {
  this.recipeService.toggleFavorite(recipe).subscribe(updated => {
    recipe.favorite = updated.favorite;
  });
}

}
