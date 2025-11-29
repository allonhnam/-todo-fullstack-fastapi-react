"use client";

import * as React from "react";
import {
  useFormContext,
  Controller,
  type FieldValues,
  type Path,
  type Control,
} from "react-hook-form";

interface FormProps {
  children: React.ReactNode;
}

export function Form({ children }: FormProps) {
  return <>{children}</>;
}

interface FormFieldProps<T extends FieldValues> {
  control: Control<T>;
  name: Path<T>;
  label?: string;
  placeholder?: string;
  type?: string;
}

export function FormField<T extends FieldValues>({
  control,
  name,
  label,
  placeholder,
  type = "text",
}: FormFieldProps<T>) {
  return (
    <Controller
      control={control}
      name={name}
      render={({ field, fieldState: { error } }) => (
        <div className="space-y-2">
          {label && (
            <label htmlFor={name} className="block text-sm font-medium">
              {label}
            </label>
          )}
          <input
            {...field}
            id={name}
            type={type}
            placeholder={placeholder}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {error && (
            <p className="text-sm text-red-500">{error.message}</p>
          )}
        </div>
      )}
    />
  );
}

