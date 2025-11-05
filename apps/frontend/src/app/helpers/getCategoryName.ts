export const getCategoryName = (categories: { key: string, name: string }[], key: string): string | undefined => {
  const category = categories.find(category => category.key === key);
  return category ? category.name : undefined;
}

export const getSubCategoryName = (categories: {
  key: string, name: string,
  subcategories: { key: string, name: string }[]
}[], key: string, subcategoryKey: string): string | undefined => {
  const category = categories.find(category => category.key === key);
  if (!category) {
    return undefined;
  }
  const subcategory = category.subcategories.find(sub => sub.key === subcategoryKey);
  return subcategory ? subcategory.name : undefined; // Return the subcategory name if found, otherwise undefined
}

