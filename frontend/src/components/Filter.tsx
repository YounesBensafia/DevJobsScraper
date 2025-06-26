import React from "react";

const Filter = () => {
  return (
    <div className="mb-6">
      <button className="filter-button">
        <span className="text-sm font-medium text-gray-700">Filtrer par :</span>
      </button>
      <button className="ml-4 filter-button">
        <span className="text-sm font-medium text-gray-700">Localisation</span>
      </button>
      <button className="ml-4 filter-button">
        <span className="text-sm font-medium text-gray-700">Salaire</span>
      </button>
    </div>
  );
};

export default Filter;
