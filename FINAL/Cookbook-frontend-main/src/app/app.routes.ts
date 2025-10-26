import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    loadComponent: () => import('./components/home/home').then(m => m.Home)
  },
  {
    path: 'add-recipe',
    loadComponent: () => import('./components/add-recipe/add-recipe').then(m => m.AddRecipe)
  },
  {
    path: 'view-recipe',
    loadComponent: () => import('./components/view-recipes/view-recipes').then(m => m.ViewRecipesComponent)
  },
  {
    path: 'recipe/:id',
    loadComponent: () => import('./components/view-detailed/view-detailed').then(m => m.ViewDetailedComponent)
  },
  {
    path: 'favorite-recipes',
    loadComponent: () => import('./components/favorite-recipes/favorite-recipes').then(m => m.FavoriteRecipesComponent)
  }
];
