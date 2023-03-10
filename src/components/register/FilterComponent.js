import { Button } from "bootstrap";
import React from "react";

export const FilterComponent = ({ filterText, onFilter, onClear }) => {
  return (
    <>
      <div className="input-group mb-3">
        <input
          type="text"
          id="search"
          className="form-control"
          placeholder="Search"
          aria-label="Search Input"
          value={filterText}
          onChange={onFilter}
          aria-describedby="basic-addon2"
        />
        <div className="input-group-append">
          <button
            className="btn btn-outline-secondary"
            type="button"
            onClick={onClear}
          >
            <i className="fas fa-times"> Button</i>
          </button>
        </div>
      </div>
    </>
  );
};
