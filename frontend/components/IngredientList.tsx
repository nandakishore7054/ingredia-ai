"use client";

import { motion } from "framer-motion";
import { X } from "lucide-react";

export default function IngredientList({
  ingredients,
  onRemove,
}: {
  ingredients: string[];
  onRemove: (ing: string) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2 mt-4">
      {ingredients.map((ing) => (
        <motion.div
          key={ing}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0 }}
          className="flex items-center gap-2 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
        >
          {ing}
          <button onClick={() => onRemove(ing)}>
            <X size={14} />
          </button>
        </motion.div>
      ))}
    </div>
  );
}
