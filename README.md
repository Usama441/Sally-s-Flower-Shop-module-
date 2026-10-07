# Sally's Flower Shop

An Odoo 19 learning module developed in small, reviewable steps.

## Current step: sell flower products

1. Install or upgrade Flower Shop. Its `sale` dependency installs the Sales app.
2. Open **Sales > Products > Flowers** and create a product. It defaults to
   **Flower** and **Sales** enabled. Use its product name as the common name.
3. Set the sales price and enter the scientific name, season dates, and watering
   information in the **Flower Details** tab.
4. Create a quotation and add an order line. Its product and variant selectors,
   and the **Catalog** button, offer only sellable flower products.

Products created through ordinary product screens default to `is_flower=False`.
The **Flower** checkbox can also classify an existing product. The Flowers
action has a fixed domain, so clearing search filters still shows only flowers.
The standard Products screen remains the full product catalog.

The filter applies to all sales orders while this module is installed. It is a
selection filter, not a server constraint: existing lines and programmatically
created lines are not rejected. Odoo's normal product and sales permissions
apply; this extension does not introduce a new security group.

The original `flower.shop.flower` learning model is retained to preserve its
records. Those records are not automatically converted to products. Sales now
uses `product.template` and its `product.product` variants; botanical details
are stored directly on the sellable product.

## Files added for sales integration

- `models/product_template.py`: the Flower checkbox and botanical fields on
  standard products.
- `models/sale_order_line.py`: extends Odoo's product selection domain with the
  flower condition. Both the template and variant selectors use this hook.
- `models/sale_order.py`: applies the same condition to the product catalog.
- `views/product_template_views.xml`: the checkbox, Flower Details tab, Flowers
  action, and menu. The action context supplies `default_is_flower=True`.
- `tests/`: checks menu defaults, product filtering, sale line creation, and
  product form inheritance.

The manifest loads the view file and declares the Sales dependency. The model
imports register these extensions; CI runs the module's tests during installation
and upgrade.

## Development checks

From this repository directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/ruff check .
.venv/bin/ruff format --check .
python3 -m compileall -q __init__.py __manifest__.py models tests
```

## Small-change Git workflow

Use one branch per task. Review the diff, run the checks, commit the related
files, and push that branch to GitHub. Open a pull request into `main` and wait
for CI to pass before merging.

```sh
git switch -c feat/next-flower-shop-step
git diff
# Run the development checks above, then stage only the related files.
git add models/flower.py
git commit -m "feat: describe the completed flower model change"
git push -u origin HEAD
```

GitHub Actions runs Python lint and formatting checks, then installs and
upgrades and tests the module in Odoo 19 against a disposable PostgreSQL database on every
push and pull request. The repository root is mounted as `flower_shop` so the
technical module name stays correct regardless of the GitHub repository name.
The database password in the workflow is only for its disposable CI service.

Deployment will be configured after a staging environment is identified.

References: [Odoo module manifests](https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html)
and [GitHub PostgreSQL services](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers).
