using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Specification : MainEntity
{
    [MaxLength(255)]
    public string? NameAr { get; set; }

    [Required]
    [MaxLength(255)]
    public string NameEn { get; set; }

    public Guid? CategoryId { get; set; }

    public string? DescriptionEn { get; set; }
    public string? DescriptionAr { get; set; }

    public Category? Category { get; set; }
    public List<Position>? Positions { get; set; } = new List<Position>();
}