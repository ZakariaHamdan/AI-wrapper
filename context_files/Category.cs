using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Category : MainEntity
{
    [MaxLength(255)]
    public string? NameAr { get; set; }

    [Required]
    [MaxLength(255)]
    public string NameEn { get; set; }

    public List<Specification>? Specifications { get; set; } = new List<Specification>();
}