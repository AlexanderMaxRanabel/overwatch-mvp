from pandas import DataFrame
from pandas.testing import assert_frame_equal

from analysis.detection.explorer.one_dimension import OneDimensionEvaluator


def test_percent_change(date_ranges_of_interest, dimension_df, mock_analysis_profile):
    rows = [
        ["mx", 26.6667, "country"],
        ["ca", 14.2857, "country"],
        ["us", 1.25, "country"],
    ]
    cols = ["dimension_value_0", "percent_change", "dimension_0"]
    expected_df = DataFrame(rows, columns=cols)

    percent_change = OneDimensionEvaluator(
        profile=mock_analysis_profile, date_ranges=date_ranges_of_interest
    )._calculate_percent_change(df=dimension_df)
    assert_frame_equal(expected_df, percent_change)


def test_calculate_contribution_to_overall_change(
    date_ranges_of_interest, dimension_df, parent_df, mock_analysis_profile
):
    # calculation =
    # 100 * (current_value - baseline_value) / abs((parent_baseline_value - parent_current_value))
    rows = [
        ["mx", 50.00, "country"],
        ["ca", 37.50, "country"],
        ["us", 12.50, "country"],
    ]
    cols = ["dimension_value_0", "contrib_to_overall_change", "dimension_0"]
    expected_df = DataFrame(rows, columns=cols)

    contr_to_change = OneDimensionEvaluator(
        profile=mock_analysis_profile, date_ranges=date_ranges_of_interest
    )._calculate_contribution_to_overall_change(current_df=dimension_df, parent_df=parent_df)

    assert_frame_equal(expected_df, contr_to_change)


def test_change_to_contribution(
    date_ranges_of_interest, dimension_df, parent_df, mock_analysis_profile
):
    # calculation =
    # 100 * ((current_value/parent_current_value) - (baseline_value/parent_baseline_value))
    # sorted by abs value.
    rows = [
        ["us", -3.6429366, "country"],
        ["mx", 2.39154616, "country"],
        ["ca", 1.25139043, "country"],
    ]

    cols = ["dimension_value_0", "change_to_contrib", "dimension_0"]
    expected_df = DataFrame(rows, columns=cols)

    change_to_contrib = OneDimensionEvaluator(
        profile=mock_analysis_profile, date_ranges=date_ranges_of_interest
    )._calculate_change_to_contribution(current_df=dimension_df, parent_df=parent_df)

    assert_frame_equal(expected_df, change_to_contrib)


def test_calculate_significance(
    date_ranges_of_interest, dimension_df, parent_df, mock_analysis_profile
):
    rows = [
        ["us", 62.7657, "country"],
        ["mx", 29.5386, "country"],
        ["ca", 7.6958, "country"],
    ]
    cols = ["dimension_value_0", "percent_significance", "dimension_0"]
    expected_df = DataFrame(rows, columns=cols)

    significance = OneDimensionEvaluator(
        profile=mock_analysis_profile, date_ranges=date_ranges_of_interest
    )._calculate_significance(current_df=dimension_df, parent_df=parent_df)

    assert_frame_equal(expected_df, significance)
