/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

// Function to resolve the JSON schema with $ref references
export default function resolveSchema(rootSchema, partialSchema) {
    if ('$ref' in partialSchema) {
        const refPath = partialSchema['$ref'].replace('#', '');
        const refSchema = getSchemaByPath(rootSchema, refPath);
        return resolveSchema(rootSchema, refSchema);
    }

    if ('properties' in partialSchema) {
        for (const propName in partialSchema.properties) {
            partialSchema.properties[propName] = resolveSchema(rootSchema, partialSchema.properties[propName]);
        }
    }

    if ('items' in partialSchema) {
        partialSchema.items = resolveSchema(rootSchema, partialSchema.items);
    }

    return partialSchema;
}

// Function to retrieve the schema by path
function getSchemaByPath(rootSchema, path) {
    const pathParts = path.split('/').filter(part => part !== '');
    let currentSchema = rootSchema;

    for (const part of pathParts) {
        if (part in currentSchema) {
            currentSchema = currentSchema[part];
        } else {
            throw new Error(`Schema path '${path}' not found in root schema.`);
        }
    }

    return currentSchema;
}